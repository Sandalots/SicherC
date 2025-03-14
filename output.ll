; ModuleID = "module"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define i32 @"main"()
{
entry:
  %".2" = bitcast [14 x i8]* @".str" to i8*
  %".3" = call i32 (i8*, ...) @"printf"(i8* %".2")
  ret i32 0
}

@".str" = internal constant [14 x i8] c"Hello, World!\00", align 1