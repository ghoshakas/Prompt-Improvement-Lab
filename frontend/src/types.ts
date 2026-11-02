export interface Task {
  id: string;
  name: string;
  description: string;
  sample_input: string;
  original_prompt: string;
  improved_prompt: string;
  explanation: string[];
}

export type Variant = "original" | "improved";

export interface RunResponse {
  output: string;
  model: string;
  latency_ms: number;
}
