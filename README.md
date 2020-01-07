# FlashM

A still simple cli flash card application 
compatible with lesson files of [Pauker](http://pauker.sourceforge.net)

The project started 2011 with inspiration from
[FlashE](https://sourceforge.net/projects/flashe/)
(2003) by Robie Lutsey

[![asciicast](https://asciinema.org/a/1G9PubduBCQKuto1ui4QicJ32.png)](https://asciinema.org/a/1G9PubduBCQKuto1ui4QicJ32)

## License

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program (see [LICENSE](LICENSE) file);
If not, see <http://www.gnu.org/licenses/>.

## Installation

This should run with both Python 2 and 3 except for the fullterm UI
which requires at least Python 3.6 (because of
[prompt-toolkit](https://github.com/jonathanslenders/python-prompt-toolkit).

```
pip install /path/to/FlashM
```

## Usage

You can run flashm with:

```
python -m flashm [options…]
```

optional arguments:              

```
  -h, --help            show this help message and exit            
  -q, --quiet           turn off verbose output                    
  -i [{cli,fullterm}], --interaction [{cli,fullterm}]              
                        UI for interaction
```

This is a beta release.
I'm happy to hear any feedback. Make a pull request or submit an issue!

Have fun and I hope this helps you learning whatever you want!
