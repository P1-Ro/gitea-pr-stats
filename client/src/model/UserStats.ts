export default interface UserStats {
  name: string;
  'opened-prs'?: number;
  'merged'?: number;
  'merged_additions'?: number;
  'merged_deletions'?: number;
  'merged_changed_files'?: number;
  'comments'?: number;
  'commented-on-prs'?: number;
  'opened_additions'?: number;
  'opened_deletions'?: number;
  'opened_changed_files'?: number;
}
