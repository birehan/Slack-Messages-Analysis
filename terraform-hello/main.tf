# main.tf

provider "local" {
}

resource "local_file" "hello" {
  content  = "Hello, World!\n"
  filename = "output.txt"
}