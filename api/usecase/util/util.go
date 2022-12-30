package util

// 配列の存在チェックメソッド
func Iscontains(s []string, e string) bool {
	for _, a := range s {
		if a == e {
			return true
		}
	}
	return false
}
