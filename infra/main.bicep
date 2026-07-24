// Oncology Care Insights Agent — Main Bicep template
// Deploy all Azure resources for the project

targetScope = 'resourceGroup'

@description('Location for all resources')
param location string = resourceGroup().location

@description('Project name prefix for resource naming')
param projectName string = 'oncologia'

@description('Environment tag')
param environment string = 'dev'

// TODO Week 6: Add modules for each resource
// - Azure AI Search
// - Azure SQL Server + Database
// - Azure Key Vault
// - Azure Functions
// - Application Insights
// - Container Apps (frontend)
