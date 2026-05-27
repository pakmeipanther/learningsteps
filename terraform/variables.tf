variable "resource_group_name" {
  type        = string
  default     = "LearningSteps-RG"
  description = "The name of our existing active resource compartment group"
}

variable "location" {
  type        = string
  default     = "westeurope"
  description = "The Azure data center geographical zone"
}

variable "project_name" {
  type        = string
  default     = "learningsteps"
  description = "Prefix applied to naming structures to avoid global naming collisions"
}

variable "acr_name" {
  type        = string
  description = "The exact name of the existing Azure Container Registry"
}

variable "cluster_name" {
  type        = string
  description = "The target deployment name for the managed AKS cluster"
}