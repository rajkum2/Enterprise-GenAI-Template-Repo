{{- define "service-chart.name" -}}
{{- .Values.serviceName -}}
{{- end -}}

{{- define "service-chart.fullname" -}}
{{- printf "%s" .Values.serviceName -}}
{{- end -}}
