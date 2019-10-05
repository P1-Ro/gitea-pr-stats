export default class Urls {
  private static BASE: string = `${window.location.origin}/api/`;

  public static generate: string = `${Urls.BASE}generate`;

  public static report: string = `${Urls.BASE}report`;

  public static repos: string = `${Urls.BASE}repos/all`;
}
