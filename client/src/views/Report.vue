<template>
  <div id="app" class="container">

    <section>
      <b-table
        :data="reports"
        :striped="true"
        :narrowed="true"
        :loading="isLoading">

        <template slot-scope="props">
          <b-table-column field="actions" label="">
            <b-button type="is-primary is-small " icon-left="eye"
                      @click="loadAndOpen(props.row.id)"></b-button>
            <b-button type="is-danger is-small" style="margin-left: 4px" icon-left="delete"
                      @click="remove(props.row.id)"></b-button>
          </b-table-column>

          <b-table-column field="name" label="Name">
            {{props.row.name}}
          </b-table-column>

          <b-table-column field="captured_at" label="Generated at" >
            {{new Date(props.row.timespan["captured_at"]).toLocaleString()}}
          </b-table-column>

          <b-table-column field="start" label="Date from" >
            {{new Date(props.row.timespan.start).toLocaleString()}}
          </b-table-column>

          <b-table-column field="end" label="Date to" >
            {{new Date(props.row.timespan.end).toLocaleString()}}
          </b-table-column>


        </template>

      </b-table>
    </section>
    <form class="section" @submit.prevent="generateReport">
      <div class="columns is-vcentered">
        <div class="column">
          <b-field label="Select from date">
            <b-datepicker
              v-model="fromDate"
              placeholder="Click to select..."
              icon="calendar-today">
            </b-datepicker>
          </b-field>
        </div>
        <div class="column">
          <b-field label="Select to date">
            <b-datepicker
              v-bind="toDate"
              placeholder="Click to select..."
              icon="calendar-today">
            </b-datepicker>
          </b-field>
        </div>
        <div class="column">
          <b-field label="Select project" ref="projectSelect">
            <b-select v-model="project" required>
              <option
                v-for="option in repos"
                :value="option"
                :key="option">
                {{ option }}
              </option>
            </b-select>
          </b-field>
        </div>
        <div class="column">
          <button type="submit" class="button is-primary" :loading="isGenerating">Generate
            report
          </button>
        </div>

      </div>

    </form>

    <section class="section">
      <b-collapse :open="isShowingReport">
        <b-table
          default-sort="opened-prs"
          default-sort-direction="desc"
          :data="report"
          :striped="true"
          :narrowed="true"
          :loading="false">

          <template slot-scope="props">

            <b-table-column field="name" label="User" sortable>
              {{props.row.name}}
            </b-table-column>

            <b-table-column field="opened-prs" label="Opened PRs" sortable>
              {{props.row["opened-prs"]}}
            </b-table-column>

            <b-table-column field="hotfixes" label="Hotfixes" sortable>
              {{props.row["hot-fix"]}}
            </b-table-column>

            <b-table-column field="merged" label="Did merge of PRs" sortable>
              {{props.row["merged"]}}
            </b-table-column>

            <b-table-column field="comments" label="Comments total" sortable>
              {{props.row["comments"]}}
            </b-table-column>

            <b-table-column field="commented-on-prs" label="Comments on PRs" sortable>
              {{props.row["commented-on-prs"]}}
            </b-table-column>

            <b-table-column field="opened_additions" label="Not merged Additions" sortable>
              {{props.row["opened_additions"]}}
            </b-table-column>


            <b-table-column field="opened_deletions" label="Not merged Deletions" sortable>
              {{props.row["opened_deletions"]}}
            </b-table-column>

            <b-table-column field="opened_changed_files" label="Not merged files" sortable>
              {{props.row["opened_changed_files"]}}
            </b-table-column>

            <b-table-column field="merged_additions" label="Merged Additions" sortable>
              {{props.row["merged_additions"]}}
            </b-table-column>

            <b-table-column field="merged_deletions" label="Merged Deletions" sortable>
              {{props.row["merged_deletions"]}}
            </b-table-column>

            <b-table-column field="merged_changed_files" label="Merged files" sortable>
              {{props.row["merged_changed_files"]}}
            </b-table-column>

          </template>

        </b-table>
      </b-collapse>
    </section>

  </div>
</template>

<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator';
    import axios from 'axios';
    import Urls from '@/util/URLs';
    import ReportMetadata from '@/model/ReportMetadata';
    import ReportContent from '@/model/ReportContent';
    import UserStats from '@/model/UserStats';

    @Component({})
    export default class Report extends Vue {

        fromDate: Date = new Date('2019-09-01');
        toDate: Date = new Date();
        project: string = '';
        reports: Array<ReportMetadata> = [];
        isLoading: boolean = true;
        isGenerating: boolean = false;
        isShowingReport: boolean = false;
        report: Array<UserStats> = [];
        repos: Array<string> = [];

        mounted() {
            this.loadRepos();
            this.loadReports();
        }

        generateReport() {

            const data = {
                from: this.fromDate,
                to: this.toDate,
                project: this.project,
            };

            this.isGenerating = true;

            axios.post<ReportMetadata>(Urls.generate, data).then((response) => {
                this.reports.push(response.data);
            }).finally(() => {
                this.isGenerating = false;
            });
        }

        remove(id: string) {
            axios.delete(`${Urls.report}/${id}`).then(() => {
                this.reports = this.reports.filter((obj: ReportMetadata) => obj.id !== id);
            });
        }

        loadAndOpen(id: string) {
            axios.get<ReportContent>(`${Urls.report}/${id}`).then((response) => {
                this.openReport(response.data);
                this.isShowingReport = true;
            }).catch(() => {
                this.isShowingReport = false;
            });
        }

        private openReport(data: ReportContent) {
            this.report = data.users;
        }

        private loadRepos() {
            axios.get<Array<string>>(Urls.repos).then((response) => {
                this.repos = response.data;
            }).finally(() => {
                this.isLoading = false;
            });
        }

        private loadReports() {
            axios.get<Array<ReportMetadata>>(`${Urls.report}/all`).then((response) => {
                this.reports = response.data;
            }).finally(() => {
                this.isLoading = false;
            });
        }

    }
</script>
