{
        "subject": {{ toJson .Subject }},
	"keyUsage": ["certSign", "crlSign"],
	"basicConstraints": {
		"isCA": true,
		"maxPathLen": 0
	},
        "crlDistributionPoints": {{toJson .Insecure.User.crlDistributionPoints }},
        "ocspServer": {{toJson .Insecure.User.ocspServer }}
}