## Requirements
* Python 2.7
* Pygame

## Running
You can run the test, with two windows and a server, running:

```shell
./test.sh 8080 # or another port
```


Or run separately

```shell
python server.py 8080 &
python game.py localhost 8080 &
python game.py localhost 8080 &
```
