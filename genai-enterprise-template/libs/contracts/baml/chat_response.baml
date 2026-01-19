// ChatResponse contract used across services

type ChatMessage {
  role: string
  content: string
}

type ToolDecision {
  tool_name: string
  approved: bool
  reason: string
}

type ChatResponse {
  id: string
  trace_id: string
  messages: ChatMessage[]
  tool_decisions: ToolDecision[]
}
