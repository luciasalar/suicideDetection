### Usage:

- Download and compile KenLM: https://github.com/kpu/kenlm
- Download and compile FastBPE: https://github.com/glample/fastBPE
- Download moses-scripts: https://github.com/marian-nmt/moses-scripts

- Open `kenlm_preproc_and_train.sh` and modify the following lines to your system's paths. Note that the lines do not appear consecutively, you need to find their locations in the script

```bash
export KENLM_BUILD_PATH=/home/dheart/uni_stuff/postdoc/suidet/kenlm/build #change that to the location on your system
export NGRAM_ORDER=4 #ngram order for kenlm
export BPE_HOME=./fastBPE #path to your fastBPE installation
export bpe_merges=15000 #number of BPE merges. Leave it at that since the dataset is small
export moses_scripts=./moses-scripts/scripts #change that to your 
```

Run the script as:
```bash
mkdir Target
./kenlm_preproc_and_train.sh Target CSV_FILES
```
Where `CSV_FILES` is a folder containing the following files (names are important):
```bash
AAll.csv #All training data for group A
BAll.csv #All training data for group B
CAll.csv #All training data for group C
DAll.csv #All training data for group D
allPtest.csv #All testing data for all classes
```