##FODT Deautostyler

Word documents ODT or not, over time develop a lot of cruft and bloat. When maintaing a large or complex wordfile, or simply one that one wants to manage changes through version control, limiting that bloat is essential. 

Most of the bloat associated with ODT documents is due to *automatic styling.* Everytime you bold a particular sentence, libreoffice or openoffice will create an individual style just for that span. You could have hundreds of lines similarly bolded, but each one will have its individual style that will be added on each addition.

The purpose of FODT Deautostyler is to enforce use of only manual styling by erasing all automatic styling (as well as cleaning up associated bloat), and to make clear where automatic styling has been used (whether even due just to absentmindedness) through the absence of its effects. It's not perfect, as review by the human eye for visual changes never is, but it operates under the theory that this is still less costly to long-term maintenance and revision of a formatted document than lack of version control or having to review each individual automatic style for removal or not.

Think of this as a halfway point between using Openoffice, and using the ever-so-slowly decaying TeX dialects. Finite control is more work, but you're able to leverage the entirety of libreoffice WYSIWYG infrastructure and not have to keep mental real estate devoted to LaTeX syntax, and your own individuals TeX macros, etc.

## Using it

```apt-get install python3-defusedxml inotify-tools```

Open an ODT file, save it as FODT. ./fodtclean.py <your file here>. If you'd like cleaning to be continuous run ./autoclean.sh <your file here>. On save, the file will be rewritten, then use libreoffice's "reload" feature under file.

You can add the "reload" action to a keybinding in libreoffice through the tools->customize... menu items.