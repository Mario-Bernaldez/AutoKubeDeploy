{{- /*
Genera el nombre base del chart
*/ -}}
{{- define "kube-manager.name" -}}
{{ .Chart.Name }}
{{- end }}

{{- /*
Genera el nombre completo del release
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
Etiqueta común para seleccionar el app
*/ -}}
{{- define "kube-manager.selectorLabels" -}}
app: {{ include "kube-manager.name" . }}
{{- end }}

{{- /*
Etiquetas comunes de metadatos
*/ -}}
{{- define "kube-manager.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
app.kubernetes.io/name: {{ include "kube-manager.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
