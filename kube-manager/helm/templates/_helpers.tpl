{{- /*
Generates the base name of the chart
*/ -}}
{{- define "kube-manager.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- /*
Generates the full name of the release
*/ -}}
{{- define "kube-manager.fullname" -}}
{{- if .Values.fullnameOverride }}
{{ .Values.fullnameOverride }}
{{- else if .Values.nameOverride }}
{{ .Values.nameOverride }}
{{- else }}
{{ printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{- /*
Common selector label for the app
*/ -}}
{{- define "kube-manager.selectorLabels" -}}
app: {{ include "kube-manager.name" . }}
{{- end }}

{{- /*
Common metadata labels
*/ -}}
{{- define "kube-manager.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
app.kubernetes.io/name: {{ include "kube-manager.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
