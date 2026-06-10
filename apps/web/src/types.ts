export type OsName = "macos" | "linux" | "windows" | "ios" | "android";

export interface RecipeSummary {
  id: string;
  product: string;
  description: string;
  categories: string[];
  platforms: OsName[];
}
