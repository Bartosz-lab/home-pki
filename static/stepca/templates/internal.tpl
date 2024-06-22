{
	"subject": {{ toJson .Subject }},
	"sans": {{ toJson .SANs }},
{{- if typeIs "*rsa.PublicKey" .Insecure.CR.PublicKey }}
	"keyUsage": ["keyEncipherment", "digitalSignature"],
{{- else }}
	"keyUsage": ["digitalSignature"],
{{- end }}
        "extKeyUsage": [
                "serverAuth", 
                "clientAuth"     
{{- if .Insecure.User.isOCSP }}
                , "OCSPSigning"
{{- end }}
        ],
        "crlDistributionPoints": {{toJson .Insecure.User.crlDistributionPoints }},
        "ocspServer": {{toJson .Insecure.User.ocspServer }}
}