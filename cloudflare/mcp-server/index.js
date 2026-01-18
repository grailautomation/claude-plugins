import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import * as z from 'zod';

// Configuration
const API_TOKEN = process.env.CLOUDFLARE_API_TOKEN;
const ACCOUNT_ID = process.env.CLOUDFLARE_ACCOUNT_ID;
const API_BASE = 'https://api.cloudflare.com/client/v4';

// Validate credentials
if (!API_TOKEN || !ACCOUNT_ID) {
  console.error('Error: CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID environment variables are required');
  process.exit(1);
}

// Generic API request function
async function cf(endpoint, method = 'GET', body = null) {
  const url = `${API_BASE}${endpoint}`;
  const options = {
    method,
    headers: {
      'Authorization': `Bearer ${API_TOKEN}`,
      'Content-Type': 'application/json'
    }
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(url, options);
  const data = await response.json();

  if (!data.success) {
    const msg = data.errors?.[0]?.message || JSON.stringify(data.errors) || 'Unknown error';
    throw new Error(`Cloudflare API: ${msg}`);
  }

  return data.result;
}

// Helper for text uploads (Workers scripts)
async function cfText(endpoint, method, text, contentType = 'application/javascript') {
  const url = `${API_BASE}${endpoint}`;
  const response = await fetch(url, {
    method,
    headers: {
      'Authorization': `Bearer ${API_TOKEN}`,
      'Content-Type': contentType
    },
    body: text
  });

  const data = await response.json();
  if (!data.success) {
    const msg = data.errors?.[0]?.message || JSON.stringify(data.errors) || 'Unknown error';
    throw new Error(`Cloudflare API: ${msg}`);
  }

  return data.result;
}

// Helper for raw responses (KV values, R2 objects)
async function cfRaw(endpoint, method = 'GET', body = null, contentType = null) {
  const url = `${API_BASE}${endpoint}`;
  const headers = {
    'Authorization': `Bearer ${API_TOKEN}`
  };
  if (contentType) {
    headers['Content-Type'] = contentType;
  }

  const options = { method, headers };
  if (body !== null) {
    options.body = body;
  }

  const response = await fetch(url, options);

  // Check if it's JSON (error response) or raw data
  const contentTypeHeader = response.headers.get('content-type') || '';
  if (contentTypeHeader.includes('application/json')) {
    const data = await response.json();
    if (data.success === false) {
      const msg = data.errors?.[0]?.message || 'Unknown error';
      throw new Error(`Cloudflare API: ${msg}`);
    }
    return data.result;
  }

  return await response.text();
}

// Response helper
function success(data) {
  return {
    content: [{
      type: 'text',
      text: typeof data === 'string' ? data : JSON.stringify(data, null, 2)
    }]
  };
}

function error(message) {
  return {
    content: [{
      type: 'text',
      text: JSON.stringify({ error: message }, null, 2)
    }]
  };
}

// Create MCP server
const server = new McpServer({
  name: 'cloudflare',
  version: '0.1.0'
});

// ============================================================
// PHASE 1: ZONES (DOMAINS)
// ============================================================

server.registerTool(
  'zones-list',
  {
    title: 'List Zones',
    description: 'List all zones (domains) in your Cloudflare account',
    inputSchema: {
      name: z.string().optional().describe('Filter by domain name'),
      page: z.number().optional().describe('Page number (default: 1)'),
      per_page: z.number().optional().describe('Results per page (default: 20, max: 50)')
    }
  },
  async ({ name, page = 1, per_page = 20 }) => {
    try {
      let endpoint = `/zones?page=${page}&per_page=${Math.min(per_page, 50)}`;
      if (name) endpoint += `&name=${encodeURIComponent(name)}`;
      const zones = await cf(endpoint);
      return success(zones.map(z => ({
        id: z.id,
        name: z.name,
        status: z.status,
        paused: z.paused,
        nameServers: z.name_servers,
        plan: z.plan?.name
      })));
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'zones-get',
  {
    title: 'Get Zone Details',
    description: 'Get detailed information about a specific zone',
    inputSchema: {
      zoneId: z.string().describe('Zone ID')
    }
  },
  async ({ zoneId }) => {
    try {
      const zone = await cf(`/zones/${zoneId}`);
      return success(zone);
    } catch (e) {
      return error(e.message);
    }
  }
);

// ============================================================
// PHASE 1: DNS RECORDS
// ============================================================

server.registerTool(
  'dns-records-list',
  {
    title: 'List DNS Records',
    description: 'List all DNS records for a zone',
    inputSchema: {
      zoneId: z.string().describe('Zone ID'),
      type: z.enum(['A', 'AAAA', 'CNAME', 'TXT', 'MX', 'NS', 'SRV', 'CAA']).optional().describe('Filter by record type'),
      name: z.string().optional().describe('Filter by record name'),
      page: z.number().optional().describe('Page number'),
      per_page: z.number().optional().describe('Results per page (max 100)')
    }
  },
  async ({ zoneId, type, name, page = 1, per_page = 100 }) => {
    try {
      let endpoint = `/zones/${zoneId}/dns_records?page=${page}&per_page=${Math.min(per_page, 100)}`;
      if (type) endpoint += `&type=${type}`;
      if (name) endpoint += `&name=${encodeURIComponent(name)}`;
      const records = await cf(endpoint);
      return success(records.map(r => ({
        id: r.id,
        type: r.type,
        name: r.name,
        content: r.content,
        ttl: r.ttl,
        proxied: r.proxied,
        priority: r.priority
      })));
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'dns-records-create',
  {
    title: 'Create DNS Record',
    description: 'Create a new DNS record',
    inputSchema: {
      zoneId: z.string().describe('Zone ID'),
      type: z.enum(['A', 'AAAA', 'CNAME', 'TXT', 'MX', 'NS', 'SRV', 'CAA']).describe('Record type'),
      name: z.string().describe('Record name (@ for root)'),
      content: z.string().describe('Record content (IP, hostname, or text)'),
      ttl: z.number().optional().describe('TTL in seconds (1 = auto)'),
      proxied: z.boolean().optional().describe('Enable Cloudflare proxy (A/AAAA/CNAME only)'),
      priority: z.number().optional().describe('Priority (MX/SRV only)')
    }
  },
  async ({ zoneId, type, name, content, ttl = 1, proxied = false, priority }) => {
    try {
      const body = { type, name, content, ttl };
      if (['A', 'AAAA', 'CNAME'].includes(type)) {
        body.proxied = proxied;
      }
      if (['MX', 'SRV'].includes(type) && priority !== undefined) {
        body.priority = priority;
      }
      const record = await cf(`/zones/${zoneId}/dns_records`, 'POST', body);
      return success({ message: 'DNS record created', record });
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'dns-records-update',
  {
    title: 'Update DNS Record',
    description: 'Update an existing DNS record',
    inputSchema: {
      zoneId: z.string().describe('Zone ID'),
      recordId: z.string().describe('DNS record ID'),
      type: z.enum(['A', 'AAAA', 'CNAME', 'TXT', 'MX', 'NS', 'SRV', 'CAA']).describe('Record type'),
      name: z.string().describe('Record name'),
      content: z.string().describe('Record content'),
      ttl: z.number().optional().describe('TTL in seconds'),
      proxied: z.boolean().optional().describe('Enable Cloudflare proxy')
    }
  },
  async ({ zoneId, recordId, type, name, content, ttl = 1, proxied }) => {
    try {
      const body = { type, name, content, ttl };
      if (proxied !== undefined && ['A', 'AAAA', 'CNAME'].includes(type)) {
        body.proxied = proxied;
      }
      const record = await cf(`/zones/${zoneId}/dns_records/${recordId}`, 'PATCH', body);
      return success({ message: 'DNS record updated', record });
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'dns-records-delete',
  {
    title: 'Delete DNS Record',
    description: 'Delete a DNS record',
    inputSchema: {
      zoneId: z.string().describe('Zone ID'),
      recordId: z.string().describe('DNS record ID')
    }
  },
  async ({ zoneId, recordId }) => {
    try {
      await cf(`/zones/${zoneId}/dns_records/${recordId}`, 'DELETE');
      return success({ message: 'DNS record deleted', recordId });
    } catch (e) {
      return error(e.message);
    }
  }
);

// ============================================================
// PHASE 1: WORKERS
// ============================================================

server.registerTool(
  'workers-list',
  {
    title: 'List Workers',
    description: 'List all Workers scripts in your account',
    inputSchema: {}
  },
  async () => {
    try {
      const workers = await cf(`/accounts/${ACCOUNT_ID}/workers/scripts`);
      return success(workers.map(w => ({
        id: w.id,
        created_on: w.created_on,
        modified_on: w.modified_on,
        etag: w.etag
      })));
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'workers-get',
  {
    title: 'Get Worker Script',
    description: 'Get a Worker script content',
    inputSchema: {
      scriptName: z.string().describe('Worker script name')
    }
  },
  async ({ scriptName }) => {
    try {
      const script = await cfRaw(`/accounts/${ACCOUNT_ID}/workers/scripts/${scriptName}`);
      return success({ scriptName, content: script });
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'workers-put',
  {
    title: 'Deploy Worker Script',
    description: 'Create or update a Worker script',
    inputSchema: {
      scriptName: z.string().describe('Worker script name'),
      script: z.string().describe('JavaScript code for the Worker')
    }
  },
  async ({ scriptName, script }) => {
    try {
      const result = await cfText(
        `/accounts/${ACCOUNT_ID}/workers/scripts/${scriptName}`,
        'PUT',
        script
      );
      return success({ message: 'Worker deployed', scriptName, result });
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'workers-delete',
  {
    title: 'Delete Worker',
    description: 'Delete a Worker script',
    inputSchema: {
      scriptName: z.string().describe('Worker script name')
    }
  },
  async ({ scriptName }) => {
    try {
      await cf(`/accounts/${ACCOUNT_ID}/workers/scripts/${scriptName}`, 'DELETE');
      return success({ message: 'Worker deleted', scriptName });
    } catch (e) {
      return error(e.message);
    }
  }
);

// ============================================================
// PHASE 2: KV NAMESPACES
// ============================================================

server.registerTool(
  'kv-namespaces-list',
  {
    title: 'List KV Namespaces',
    description: 'List all KV namespaces in your account',
    inputSchema: {
      page: z.number().optional().describe('Page number'),
      per_page: z.number().optional().describe('Results per page')
    }
  },
  async ({ page = 1, per_page = 100 }) => {
    try {
      const namespaces = await cf(`/accounts/${ACCOUNT_ID}/storage/kv/namespaces?page=${page}&per_page=${per_page}`);
      return success(namespaces);
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'kv-namespace-create',
  {
    title: 'Create KV Namespace',
    description: 'Create a new KV namespace',
    inputSchema: {
      title: z.string().describe('Namespace title')
    }
  },
  async ({ title }) => {
    try {
      const ns = await cf(`/accounts/${ACCOUNT_ID}/storage/kv/namespaces`, 'POST', { title });
      return success({ message: 'KV namespace created', namespace: ns });
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'kv-keys-list',
  {
    title: 'List KV Keys',
    description: 'List keys in a KV namespace',
    inputSchema: {
      namespaceId: z.string().describe('KV namespace ID'),
      prefix: z.string().optional().describe('Filter by key prefix'),
      limit: z.number().optional().describe('Maximum keys to return')
    }
  },
  async ({ namespaceId, prefix, limit = 1000 }) => {
    try {
      let endpoint = `/accounts/${ACCOUNT_ID}/storage/kv/namespaces/${namespaceId}/keys?limit=${limit}`;
      if (prefix) endpoint += `&prefix=${encodeURIComponent(prefix)}`;
      const keys = await cf(endpoint);
      return success(keys);
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'kv-get',
  {
    title: 'Get KV Value',
    description: 'Get a value from KV storage',
    inputSchema: {
      namespaceId: z.string().describe('KV namespace ID'),
      key: z.string().describe('Key to retrieve')
    }
  },
  async ({ namespaceId, key }) => {
    try {
      const value = await cfRaw(`/accounts/${ACCOUNT_ID}/storage/kv/namespaces/${namespaceId}/values/${encodeURIComponent(key)}`);
      return success({ key, value });
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'kv-put',
  {
    title: 'Put KV Value',
    description: 'Store a value in KV storage',
    inputSchema: {
      namespaceId: z.string().describe('KV namespace ID'),
      key: z.string().describe('Key to store'),
      value: z.string().describe('Value to store'),
      expirationTtl: z.number().optional().describe('TTL in seconds')
    }
  },
  async ({ namespaceId, key, value, expirationTtl }) => {
    try {
      let endpoint = `/accounts/${ACCOUNT_ID}/storage/kv/namespaces/${namespaceId}/values/${encodeURIComponent(key)}`;
      if (expirationTtl) endpoint += `?expiration_ttl=${expirationTtl}`;
      await cfRaw(endpoint, 'PUT', value, 'text/plain');
      return success({ message: 'Value stored', key });
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'kv-delete',
  {
    title: 'Delete KV Value',
    description: 'Delete a value from KV storage',
    inputSchema: {
      namespaceId: z.string().describe('KV namespace ID'),
      key: z.string().describe('Key to delete')
    }
  },
  async ({ namespaceId, key }) => {
    try {
      await cf(`/accounts/${ACCOUNT_ID}/storage/kv/namespaces/${namespaceId}/values/${encodeURIComponent(key)}`, 'DELETE');
      return success({ message: 'Value deleted', key });
    } catch (e) {
      return error(e.message);
    }
  }
);

// ============================================================
// PHASE 2: R2 STORAGE
// ============================================================

server.registerTool(
  'r2-buckets-list',
  {
    title: 'List R2 Buckets',
    description: 'List all R2 buckets in your account',
    inputSchema: {}
  },
  async () => {
    try {
      const buckets = await cf(`/accounts/${ACCOUNT_ID}/r2/buckets`);
      return success(buckets.buckets || buckets);
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'r2-bucket-create',
  {
    title: 'Create R2 Bucket',
    description: 'Create a new R2 bucket',
    inputSchema: {
      name: z.string().describe('Bucket name (lowercase, alphanumeric, hyphens)')
    }
  },
  async ({ name }) => {
    try {
      const bucket = await cf(`/accounts/${ACCOUNT_ID}/r2/buckets`, 'POST', { name });
      return success({ message: 'R2 bucket created', bucket });
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'r2-bucket-delete',
  {
    title: 'Delete R2 Bucket',
    description: 'Delete an R2 bucket (must be empty)',
    inputSchema: {
      name: z.string().describe('Bucket name')
    }
  },
  async ({ name }) => {
    try {
      await cf(`/accounts/${ACCOUNT_ID}/r2/buckets/${name}`, 'DELETE');
      return success({ message: 'R2 bucket deleted', name });
    } catch (e) {
      return error(e.message);
    }
  }
);

// ============================================================
// PHASE 2: D1 DATABASE
// ============================================================

server.registerTool(
  'd1-databases-list',
  {
    title: 'List D1 Databases',
    description: 'List all D1 databases in your account',
    inputSchema: {}
  },
  async () => {
    try {
      const databases = await cf(`/accounts/${ACCOUNT_ID}/d1/database`);
      return success(databases);
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'd1-database-create',
  {
    title: 'Create D1 Database',
    description: 'Create a new D1 database',
    inputSchema: {
      name: z.string().describe('Database name')
    }
  },
  async ({ name }) => {
    try {
      const db = await cf(`/accounts/${ACCOUNT_ID}/d1/database`, 'POST', { name });
      return success({ message: 'D1 database created', database: db });
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'd1-database-delete',
  {
    title: 'Delete D1 Database',
    description: 'Delete a D1 database',
    inputSchema: {
      databaseId: z.string().describe('Database ID')
    }
  },
  async ({ databaseId }) => {
    try {
      await cf(`/accounts/${ACCOUNT_ID}/d1/database/${databaseId}`, 'DELETE');
      return success({ message: 'D1 database deleted', databaseId });
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'd1-query',
  {
    title: 'Execute D1 Query',
    description: 'Execute a SQL query against a D1 database',
    inputSchema: {
      databaseId: z.string().describe('Database ID'),
      sql: z.string().describe('SQL query to execute'),
      params: z.array(z.string()).optional().describe('Query parameters for prepared statement')
    }
  },
  async ({ databaseId, sql, params = [] }) => {
    try {
      const result = await cf(`/accounts/${ACCOUNT_ID}/d1/database/${databaseId}/query`, 'POST', {
        sql,
        params
      });
      return success(result);
    } catch (e) {
      return error(e.message);
    }
  }
);

// ============================================================
// BONUS: PAGES
// ============================================================

server.registerTool(
  'pages-projects-list',
  {
    title: 'List Pages Projects',
    description: 'List all Cloudflare Pages projects',
    inputSchema: {}
  },
  async () => {
    try {
      const projects = await cf(`/accounts/${ACCOUNT_ID}/pages/projects`);
      return success(projects.map(p => ({
        name: p.name,
        subdomain: p.subdomain,
        domains: p.domains,
        created_on: p.created_on,
        production_branch: p.production_branch
      })));
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'pages-project-get',
  {
    title: 'Get Pages Project',
    description: 'Get details of a Pages project',
    inputSchema: {
      projectName: z.string().describe('Project name')
    }
  },
  async ({ projectName }) => {
    try {
      const project = await cf(`/accounts/${ACCOUNT_ID}/pages/projects/${projectName}`);
      return success(project);
    } catch (e) {
      return error(e.message);
    }
  }
);

// ============================================================
// BONUS: WORKER ROUTES
// ============================================================

server.registerTool(
  'worker-routes-list',
  {
    title: 'List Worker Routes',
    description: 'List all Worker routes for a zone',
    inputSchema: {
      zoneId: z.string().describe('Zone ID')
    }
  },
  async ({ zoneId }) => {
    try {
      const routes = await cf(`/zones/${zoneId}/workers/routes`);
      return success(routes);
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'worker-route-create',
  {
    title: 'Create Worker Route',
    description: 'Create a route that maps to a Worker',
    inputSchema: {
      zoneId: z.string().describe('Zone ID'),
      pattern: z.string().describe('URL pattern (e.g., "example.com/*")'),
      scriptName: z.string().describe('Worker script name')
    }
  },
  async ({ zoneId, pattern, scriptName }) => {
    try {
      const route = await cf(`/zones/${zoneId}/workers/routes`, 'POST', {
        pattern,
        script: scriptName
      });
      return success({ message: 'Worker route created', route });
    } catch (e) {
      return error(e.message);
    }
  }
);

server.registerTool(
  'worker-route-delete',
  {
    title: 'Delete Worker Route',
    description: 'Delete a Worker route',
    inputSchema: {
      zoneId: z.string().describe('Zone ID'),
      routeId: z.string().describe('Route ID')
    }
  },
  async ({ zoneId, routeId }) => {
    try {
      await cf(`/zones/${zoneId}/workers/routes/${routeId}`, 'DELETE');
      return success({ message: 'Worker route deleted', routeId });
    } catch (e) {
      return error(e.message);
    }
  }
);

// ============================================================
// CONNECT VIA STDIO
// ============================================================

const transport = new StdioServerTransport();
await server.connect(transport);
