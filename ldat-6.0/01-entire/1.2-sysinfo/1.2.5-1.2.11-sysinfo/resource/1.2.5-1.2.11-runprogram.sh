###########################################################
# 1.2.5-1.2.10-runprogram.sh
# Use this script to run program VisualOutput
# $1: user password
# $2: output directory
###########################################################

tag="1.2.5-1.2.10-runprogram.sh"

function enableDynamicLibs()
{
  chmod +x -R *
}

function runProgram()
{
    $1 $2
}

function main()
{
  if [ $# -ne 3 ]; then
      echo "$tag Arguments Error; Usage: echo passwd | sudo -S ./1.2.5-1.2.10-runprogram.sh programPath outputDir dynamicDirPath"
      return 1
  fi

  if [ `whoami`x != "root"x  ]; then
      echo "$tag Please running under root env"
      return 2
  fi

  echo "Right arguments, \$1=$1, \$2=$2, \$3=$3"
  enableDynamicLibs

  if [ $? -ne 0 ]; then
    echo "${tag}: Cannot enableDynamicLibs"
    return 1
  fi

  # setting environment
  libPath="${3}"
  export LD_LIBRARY_PATH=$libPath:$LD_LIBRARY_PATH
  envSetting=`env | grep LD_LIBRARY_PATH | grep "${libPath}"`
  if [ "${envSetting}"x = ""x ]; then
    echo "$tag: Error: Cannot set environment varible for Qt"
    return 3
  fi
  
  echo "in 1.2.5: ${envSetting}"
  runProgram $1 $2
}

main "$@"
