#!/usr/bin/env node
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import * as z from 'zod';

const API_URL = 'https://api.namecheap.com/xml.response';

// Get credentials from environment
const API_USER = process.env.NAMECHEAP_API_USER;
const API_KEY = process.env.NAMECHEAP_API_KEY;
const USERNAME = process.env.NAMECHEAP_USERNAME || API_USER;

if (!API_USER || !API_KEY) {
  console.error('Error: NAMECHEAP_API_USER and NAMECHEAP_API_KEY environment variables are required');
  process.exit(1);
}

// Get client IP for API authentication
async function getClientIp() {
  try {
    const response = await fetch('https://api.ipify.org?format=json');
    const data = await response.json();
    return data.ip;
  } catch {
    // Fallback - Namecheap requires a valid IP
    throw new Error('Could not determine client IP address');
  }
}

// Make API request to Namecheap
async function namecheapRequest(command, params = {}) {
  const clientIp = await getClientIp();

  const queryParams = new URLSearchParams({
    ApiUser: API_USER,
    ApiKey: API_KEY,
    UserName: USERNAME,
    ClientIp: clientIp,
    Command: command,
    ...params
  });

  const response = await fetch(`${API_URL}?${queryParams}`);
  const xml = await response.text();

  // Check for API errors
  if (xml.includes('Status="ERROR"')) {
    const errorMatch = xml.match(/<Error[^>]*>([^<]+)<\/Error>/);
    const error = errorMatch ? errorMatch[1] : 'Unknown API error';
    throw new Error(`Namecheap API error: ${error}`);
  }

  return xml;
}

// Parse domain from SLD.TLD format
function parseDomain(domain) {
  const parts = domain.toLowerCase().split('.');
  if (parts.length < 2) {
    throw new Error(`Invalid domain format: ${domain}. Expected format: example.com`);
  }
  // Handle multi-part TLDs like .co.uk
  const tld = parts.slice(-1)[0];
  const sld = parts.slice(0, -1).join('.');
  return { sld, tld };
}

// Parse XML helper functions
function extractValue(xml, tag) {
  const match = xml.match(new RegExp(`<${tag}[^>]*>([^<]*)</${tag}>`, 'i'));
  return match ? match[1] : null;
}

function extractAttribute(xml, tag, attr) {
  const match = xml.match(new RegExp(`<${tag}[^>]*\\s${attr}="([^"]*)"`, 'i'));
  return match ? match[1] : null;
}

function extractAllAttributes(xml, tag) {
  const regex = new RegExp(`<${tag}([^>]*)`, 'gi');
  const results = [];
  let match;
  while ((match = regex.exec(xml)) !== null) {
    const attrs = {};
    const attrRegex = /(\w+)="([^"]*)"/g;
    let attrMatch;
    while ((attrMatch = attrRegex.exec(match[1])) !== null) {
      attrs[attrMatch[1]] = attrMatch[2];
    }
    if (Object.keys(attrs).length > 0) {
      results.push(attrs);
    }
  }
  return results;
}

// Create MCP server
const server = new McpServer({
  name: 'namecheap',
  version: '0.1.0'
});

// Tool: List all domains
server.registerTool(
  'list-domains',
  {
    title: 'List Domains',
    description: 'Get all domains in your Namecheap account',
    inputSchema: {
      page: z.number().optional().describe('Page number (default: 1)'),
      pageSize: z.number().optional().describe('Results per page (default: 20, max: 100)')
    }
  },
  async ({ page = 1, pageSize = 20 }) => {
    const xml = await namecheapRequest('namecheap.domains.getList', {
      Page: String(page),
      PageSize: String(Math.min(pageSize, 100))
    });

    const domains = extractAllAttributes(xml, 'Domain');
    const formattedDomains = domains.map(d => ({
      name: d.Name,
      expires: d.Expires,
      isExpired: d.IsExpired === 'true',
      isLocked: d.IsLocked === 'true',
      autoRenew: d.AutoRenew === 'true',
      whoisGuard: d.WhoisGuard
    }));

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(formattedDomains, null, 2)
      }]
    };
  }
);

// Tool: Get domain info
server.registerTool(
  'get-domain-info',
  {
    title: 'Get Domain Info',
    description: 'Get detailed information for a specific domain including status, expiry, and nameservers',
    inputSchema: {
      domain: z.string().describe('Domain name (e.g., example.com)')
    }
  },
  async ({ domain }) => {
    const xml = await namecheapRequest('namecheap.domains.getInfo', {
      DomainName: domain
    });

    const info = {
      domain: extractAttribute(xml, 'DomainGetInfoResult', 'DomainName'),
      status: extractAttribute(xml, 'DomainGetInfoResult', 'Status'),
      created: extractAttribute(xml, 'DomainDetails', 'CreatedDate') || extractValue(xml, 'CreatedDate'),
      expires: extractAttribute(xml, 'DomainDetails', 'ExpiredDate') || extractValue(xml, 'ExpiredDate'),
      isLocked: extractAttribute(xml, 'DomainGetInfoResult', 'IsLocked') === 'true',
      isExpired: extractAttribute(xml, 'DomainGetInfoResult', 'IsExpired') === 'true',
      autoRenew: extractAttribute(xml, 'DomainGetInfoResult', 'AutoRenew') === 'true'
    };

    // Extract nameservers
    const nsMatch = xml.match(/<DnsDetails[^>]*>([\s\S]*?)<\/DnsDetails>/i);
    if (nsMatch) {
      const nameservers = [];
      const nsRegex = /<Nameserver>([^<]+)<\/Nameserver>/gi;
      let nsResult;
      while ((nsResult = nsRegex.exec(nsMatch[1])) !== null) {
        nameservers.push(nsResult[1]);
      }
      info.nameservers = nameservers;
      info.usingNamecheapDNS = xml.includes('ProviderType="CUSTOM"') ? false : true;
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(info, null, 2)
      }]
    };
  }
);

// Tool: Get DNS hosts
server.registerTool(
  'get-dns-hosts',
  {
    title: 'Get DNS Hosts',
    description: 'Get all DNS host records for a domain',
    inputSchema: {
      domain: z.string().describe('Domain name (e.g., example.com)')
    }
  },
  async ({ domain }) => {
    const { sld, tld } = parseDomain(domain);

    const xml = await namecheapRequest('namecheap.domains.dns.getHosts', {
      SLD: sld,
      TLD: tld
    });

    const hosts = extractAllAttributes(xml, 'host');
    const formattedHosts = hosts.map(h => ({
      hostId: h.HostId,
      name: h.Name,
      type: h.Type,
      address: h.Address,
      ttl: h.TTL,
      mxPref: h.MXPref || null
    }));

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(formattedHosts, null, 2)
      }]
    };
  }
);

// Tool: Set DNS host
server.registerTool(
  'set-dns-host',
  {
    title: 'Set DNS Host',
    description: 'Add or update a DNS host record. Note: This replaces ALL existing records, so include existing records you want to keep.',
    inputSchema: {
      domain: z.string().describe('Domain name (e.g., example.com)'),
      records: z.array(z.object({
        name: z.string().describe('Host name (@ for root, www, mail, etc.)'),
        type: z.enum(['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'URL', 'URL301', 'FRAME']).describe('Record type'),
        address: z.string().describe('Record value (IP address, hostname, or text)'),
        ttl: z.number().optional().describe('TTL in seconds (default: 1800)'),
        mxPref: z.number().optional().describe('MX priority (required for MX records)')
      })).describe('Array of DNS records to set')
    }
  },
  async ({ domain, records }) => {
    const { sld, tld } = parseDomain(domain);

    const params = {
      SLD: sld,
      TLD: tld
    };

    records.forEach((record, i) => {
      const idx = i + 1;
      params[`HostName${idx}`] = record.name;
      params[`RecordType${idx}`] = record.type;
      params[`Address${idx}`] = record.address;
      params[`TTL${idx}`] = record.ttl || 1800;
      if (record.type === 'MX' && record.mxPref !== undefined) {
        params[`MXPref${idx}`] = record.mxPref;
      }
    });

    const xml = await namecheapRequest('namecheap.domains.dns.setHosts', params);

    const isSuccess = xml.includes('IsSuccess="true"');

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          success: isSuccess,
          domain: domain,
          recordsSet: records.length,
          message: isSuccess ? 'DNS records updated successfully' : 'Failed to update DNS records'
        }, null, 2)
      }]
    };
  }
);

// Tool: Delete DNS host (by setting all other records)
server.registerTool(
  'delete-dns-host',
  {
    title: 'Delete DNS Host',
    description: 'Delete a DNS host record by name and type. Retrieves current records and re-sets without the specified one.',
    inputSchema: {
      domain: z.string().describe('Domain name (e.g., example.com)'),
      name: z.string().describe('Host name to delete (@ for root, www, etc.)'),
      type: z.enum(['A', 'AAAA', 'CNAME', 'MX', 'TXT', 'URL', 'URL301', 'FRAME']).describe('Record type to delete')
    }
  },
  async ({ domain, name, type }) => {
    const { sld, tld } = parseDomain(domain);

    // First get current records
    const getXml = await namecheapRequest('namecheap.domains.dns.getHosts', {
      SLD: sld,
      TLD: tld
    });

    const currentHosts = extractAllAttributes(getXml, 'host');
    const filteredHosts = currentHosts.filter(h =>
      !(h.Name.toLowerCase() === name.toLowerCase() && h.Type === type)
    );

    if (filteredHosts.length === currentHosts.length) {
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: false,
            message: `Record not found: ${name} (${type})`
          }, null, 2)
        }]
      };
    }

    // If no records left, we need at least one record
    if (filteredHosts.length === 0) {
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: false,
            message: 'Cannot delete the last DNS record. At least one record must remain.'
          }, null, 2)
        }]
      };
    }

    // Set the filtered records
    const params = {
      SLD: sld,
      TLD: tld
    };

    filteredHosts.forEach((host, i) => {
      const idx = i + 1;
      params[`HostName${idx}`] = host.Name;
      params[`RecordType${idx}`] = host.Type;
      params[`Address${idx}`] = host.Address;
      params[`TTL${idx}`] = host.TTL || 1800;
      if (host.Type === 'MX' && host.MXPref) {
        params[`MXPref${idx}`] = host.MXPref;
      }
    });

    const xml = await namecheapRequest('namecheap.domains.dns.setHosts', params);
    const isSuccess = xml.includes('IsSuccess="true"');

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          success: isSuccess,
          message: isSuccess ? `Deleted ${name} (${type}) record` : 'Failed to delete record',
          remainingRecords: filteredHosts.length
        }, null, 2)
      }]
    };
  }
);

// Tool: Get nameservers
server.registerTool(
  'get-nameservers',
  {
    title: 'Get Nameservers',
    description: 'Get current nameservers for a domain',
    inputSchema: {
      domain: z.string().describe('Domain name (e.g., example.com)')
    }
  },
  async ({ domain }) => {
    const { sld, tld } = parseDomain(domain);

    const xml = await namecheapRequest('namecheap.domains.dns.getList', {
      SLD: sld,
      TLD: tld
    });

    const nameservers = [];
    const nsRegex = /<Nameserver>([^<]+)<\/Nameserver>/gi;
    let match;
    while ((match = nsRegex.exec(xml)) !== null) {
      nameservers.push(match[1]);
    }

    const isUsingDefault = xml.includes('IsUsingOurDNS="true"');

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          domain: domain,
          nameservers: nameservers,
          usingNamecheapDNS: isUsingDefault
        }, null, 2)
      }]
    };
  }
);

// Tool: Set custom nameservers
server.registerTool(
  'set-nameservers',
  {
    title: 'Set Nameservers',
    description: 'Set custom nameservers for a domain (e.g., Cloudflare nameservers)',
    inputSchema: {
      domain: z.string().describe('Domain name (e.g., example.com)'),
      nameservers: z.array(z.string()).min(2).max(5).describe('Array of nameserver hostnames (e.g., ["ns1.cloudflare.com", "ns2.cloudflare.com"])')
    }
  },
  async ({ domain, nameservers }) => {
    const { sld, tld } = parseDomain(domain);

    const xml = await namecheapRequest('namecheap.domains.dns.setCustom', {
      SLD: sld,
      TLD: tld,
      Nameservers: nameservers.join(',')
    });

    const isSuccess = xml.includes('Update="true"') || xml.includes('IsSuccess="true"');

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          success: isSuccess,
          domain: domain,
          nameservers: nameservers,
          message: isSuccess
            ? 'Nameservers updated successfully. DNS propagation may take up to 48 hours.'
            : 'Failed to update nameservers'
        }, null, 2)
      }]
    };
  }
);

// Tool: Set default nameservers
server.registerTool(
  'set-default-nameservers',
  {
    title: 'Set Default Nameservers',
    description: 'Reset domain to use Namecheap default nameservers',
    inputSchema: {
      domain: z.string().describe('Domain name (e.g., example.com)')
    }
  },
  async ({ domain }) => {
    const { sld, tld } = parseDomain(domain);

    const xml = await namecheapRequest('namecheap.domains.dns.setDefault', {
      SLD: sld,
      TLD: tld
    });

    const isSuccess = xml.includes('Updated="true"') || xml.includes('IsSuccess="true"');

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          success: isSuccess,
          domain: domain,
          message: isSuccess
            ? 'Domain reset to Namecheap default nameservers'
            : 'Failed to reset nameservers'
        }, null, 2)
      }]
    };
  }
);

// Connect via stdio transport
const transport = new StdioServerTransport();
await server.connect(transport);
