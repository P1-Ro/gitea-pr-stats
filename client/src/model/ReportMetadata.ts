export default interface ReportMetadata {
  id: string;
  name: string;
  timespan : {
      'captured_at': Date;
      start: Date;
      end: Date;
  }
}
