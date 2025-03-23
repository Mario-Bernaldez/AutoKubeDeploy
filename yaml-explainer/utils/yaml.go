package utils

import (
	"gopkg.in/yaml.v3"
)

func IsValidYAML(input string) bool {
	var out interface{}
	return yaml.Unmarshal([]byte(input), &out) == nil
}
