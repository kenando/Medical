import { z } from "zod"

export const AnalyzeSchema = z.object({
  video: z.instanceof(File)
})
