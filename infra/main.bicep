// Oncology Care Insights Agent — Main Bicep Template
// Deploys all Azure resources for the project

targetScope = 'resourceGroup'

@description('Location for all resources')
param location string = resourceGroup().location

@description('Project name prefix')
param projectName string = 'oncology'

@description('Environment')
param environment string = 'dev'

@description('SQL admin login')
param sqlAdminLogin string = 'oncologyadmin'

@description('SQL admin password')
@secure()
param sqlAdminPassword string

// ── AZURE AI SEARCH ───────────────────────────────────────
resource searchService 'Microsoft.Search/searchServices@2023-11-01' = {
  name: '${projectName}-search'
  location: location
  sku: {
    name: 'free'
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
  }
  tags: {
    project: projectName
    environment: environment
  }
}

// ── AZURE SQL SERVER ──────────────────────────────────────
resource sqlServer 'Microsoft.Sql/servers@2023-05-01-preview' = {
  name: '${projectName}-sql-server'
  location: 'centralus'
  properties: {
    administratorLogin: sqlAdminLogin
    administratorLoginPassword: sqlAdminPassword
    version: '12.0'
  }
  tags: {
    project: projectName
    environment: environment
  }
}

// ── AZURE SQL DATABASE ────────────────────────────────────
resource sqlDatabase 'Microsoft.Sql/servers/databases@2023-05-01-preview' = {
  parent: sqlServer
  name: '${projectName}-patients'
  location: 'centralus'
  sku: {
    name: 'Basic'
    tier: 'Basic'
    capacity: 5
  }
  tags: {
    project: projectName
    environment: environment
  }
}

// ── SQL FIREWALL — ALLOW AZURE SERVICES ──────────────────
resource sqlFirewallAzure 'Microsoft.Sql/servers/firewallRules@2023-05-01-preview' = {
  parent: sqlServer
  name: 'AllowAzureServices'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

// ── KEY VAULT ─────────────────────────────────────────────
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: '${projectName}-kv-2026'
  location: 'centralus'
  properties: {
    sku: {
      family: 'A'
      name: 'standard'
    }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
    enableSoftDelete: true
    softDeleteRetentionInDays: 7
  }
  tags: {
    project: projectName
    environment: environment
  }
}

// ── CONTENT SAFETY ────────────────────────────────────────
resource contentSafety 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: '${projectName}-content-safety'
  location: location
  kind: 'ContentSafety'
  sku: {
    name: 'F0'
  }
  properties: {
    customSubDomainName: '${projectName}-content-safety'
    publicNetworkAccess: 'Enabled'
  }
  tags: {
    project: projectName
    environment: environment
  }
}

// ── OUTPUTS ───────────────────────────────────────────────
output searchEndpoint string = 'https://${searchService.name}.search.windows.net'
output sqlServerFqdn string = sqlServer.properties.fullyQualifiedDomainName
output keyVaultUri string = keyVault.properties.vaultUri
output contentSafetyEndpoint string = contentSafety.properties.endpoint