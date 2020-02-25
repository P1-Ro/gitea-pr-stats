import UserStats from '@/model/UserStats';
import ReportMetadata from '@/model/ReportMetadata';

export default interface ReportContent extends ReportMetadata {
  users: Array<UserStats>;
}
