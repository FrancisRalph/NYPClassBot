setlocal enableDelayedExpansion
for /F "tokens=*" %%A in (.gitignore) do (
    set x=%%A
    set y=!x:~1!
    git rm -r --cached !y!
)