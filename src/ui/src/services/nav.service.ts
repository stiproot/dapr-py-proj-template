import { Router } from "vue-router";

export class NavService {

  private _router: Router;

  constructor(router: Router) {
    this._router = router;
    this.goToSettings = this.goToSettings.bind(this);
  }

  goToProjects() {
    this._router.push({ name: "projects" });
  }

  goToSettings() {
    this._router.push({
      name: "settings",
    });
  }

  getRouteParam(param: string) {
    return this._router.currentRoute.value.params[param];
  }

  replace(query: any) {
    this._router.replace(query);
  }
}
