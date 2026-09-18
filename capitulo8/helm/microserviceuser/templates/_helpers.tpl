{{/*
Nombre de la aplicación.
*/}}
{{- define "microserviceuser.name" -}}
{{- .Chart.Name -}}
{{- end }}


{{/*
Nombre completo de los recursos.
*/}}
{{- define "microserviceuser.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end }}