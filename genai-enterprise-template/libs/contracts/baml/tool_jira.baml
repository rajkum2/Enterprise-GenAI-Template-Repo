// Jira tool input contract

type JiraCreateTicketInput {
  project_key: string
  summary: string
  description: string
  priority: string
  labels: string[]
}
