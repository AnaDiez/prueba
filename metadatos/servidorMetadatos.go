package main
import (
  "fmt"
  "net/http"
  "os"
  "os/exec"
  "syscall"
)

const  LOG_FILE = "/app/logging/log/metadatos.privapp.log"

var apk_path string
var app string
const defaultFailedCode = 10
var testing_label string

type resp struct {
  Ok  bool
  Msg string
}


func manejador(w http.ResponseWriter, r *http.Request){
  host, _ := os.Hostname()
  fmt.Fprintf(w, "Hostname: %s\n", host)
  fmt.Fprintf(w,"Metadata server is working!")
}


func extractApk(w http.ResponseWriter, r *http.Request){
  app := r.FormValue("app")
  apk_path := r.FormValue("apk_path")
  fmt.Fprintf(w,"esta es la app: %s \n", app)
  fmt.Fprintf(w,"este es el path: %s \n", apk_path)
  version := r.FormValue("version")
  testing_label := r.FormValue("testing_label")

  arg1 := "python"
  arg2 := "extractApk.py"
  arg3 := apk_path
  arg4 := app
  arg5 := version
  arg6 := testing_label
  pwdCmd := exec.Command(arg1, arg2, arg3 , arg4, arg5, arg6)
  pwdOut, err := pwdCmd.Output()
  fmt.Println("> python extractApk.py")
  fmt.Println(string(pwdOut))
  if err != nil {
      fmt.Println(err)
  } 
}

func certInfo(w http.ResponseWriter, r *http.Request){
  app := r.FormValue("app")
  version := r.FormValue("version")
  testing_label := r.FormValue("testing_label")
  fmt.Fprintf(w,"esta es la app: %s \n", app)

  arg1 := "python"
  arg2 := "certInfo.py"
  arg3 := app
  arg4 := version
  arg5 := testing_label
  pwdCmd := exec.Command(arg1, arg2, arg3, arg4, arg5)
  pwdOut, err := pwdCmd.Output()
  fmt.Println("> python certInfo.py")
  fmt.Println(string(pwdOut)) 
  if err != nil {
      fmt.Println(err)
  }
}

func extractPermissions(w http.ResponseWriter, r *http.Request){
  app := r.FormValue("app")
  version := r.FormValue("version")
  testing_label := r.FormValue("testing_label")
  fmt.Fprintf(w,"esta es la app: %s \n", app)

  arg1 := "python"
  arg2 := "extractPermissions.py"
  arg3 := app
  arg4 := version
  arg5 := testing_label
  pwdCmd := exec.Command(arg1, arg2, arg3, arg4, arg5)
  pwdOut, err := pwdCmd.Output()
  fmt.Println("> python extractPermissions.py")
  fmt.Println(string(pwdOut)) 
  if err != nil {
      fmt.Println(err)
  }
}

func hashes(w http.ResponseWriter, r *http.Request){
  app := r.FormValue("app")
  apk_path := r.FormValue("apk_path")
  version := r.FormValue("version")
  testing_label := r.FormValue("testing_label")
  fmt.Fprintf(w,"esta es la app: %s \n", app)
  fmt.Fprintf(w,"este es el path: %s \n", apk_path)


  arg1 := "python"
  arg2 := "hashes.py"
  arg3 := apk_path
  arg4 := app
  arg5 := version
  arg6 := testing_label
  pwdCmd := exec.Command(arg1, arg2, arg3 , arg4, arg5, arg6)
  pwdOut, err := pwdCmd.Output()
  fmt.Println("> python hashes.py")
  fmt.Println(string(pwdOut)) 
  if err != nil {
      fmt.Println(err)
  }
}

func nativeCode(w http.ResponseWriter, r *http.Request){
  app := r.FormValue("app")
  version := r.FormValue("version")
  testing_label := r.FormValue("testing_label")
  fmt.Fprintf(w,"esta es la app: %s \n", app)

  arg1 := "python"
  arg2 := "nativeCode.py"
  arg3 := app
  arg4 := version
  arg5 := testing_label
  pwdCmd := exec.Command(arg1, arg2, arg3, arg4, arg5)
  pwdOut, err := pwdCmd.Output()
  fmt.Println("> python nativeCode.py")
  fmt.Println(string(pwdOut))
  if err != nil {
      fmt.Println(err)
  }
}

func main(){
  port := fmt.Sprintf(":%v", os.Args[1])
  http.HandleFunc("/", manejador)
  http.HandleFunc("/extractApk", extractApk)
  http.HandleFunc("/certInfo", certInfo)
  http.HandleFunc("/extractPermissions", extractPermissions)
  http.HandleFunc("/hashes", hashes)
  http.HandleFunc("/nativeCode", nativeCode)
  fmt.Println("El servidor se encuentra en ejecución")
  fmt.Println("Listening in", port)
  http.ListenAndServe(port, nil)
}

func RunCommand(name string, arg ...string) (exitCode int){
  cmd := exec.Command(name, arg...)
    
  if err := cmd.Run(); err != nil {
    //try to get exit code
    if exitError, ok := err.(*exec.ExitError); ok{
      ws := exitError.Sys().(syscall.WaitStatus)
                exitCode = ws.ExitStatus()
    }else{
      exitCode = defaultFailedCode
    }
  } else {
    //success, exitCode 0
    ws := cmd.ProcessState.Sys().(syscall.WaitStatus)
    exitCode = ws.ExitStatus()
  }
  return
}

