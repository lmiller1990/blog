# Running

- download genomes with `./download.sh`
- rename them to have adenovirus type in header: `./rename.sh`
- see ANI / AF within a single group: `./dist.sh`

```
Adenovirus A ANI / AF: 88.9234, 96.904
Adenovirus B ANI / AF: 89.471, 92.9894
Adenovirus C ANI / AF: 96.9542, 97.0118
Adenovirus D ANI / AF: 96.2298, 98.991
Adenovirus E ANI / AF: 93.9598, 95.4397
Adenovirus F ANI / AF: 89.6711, 91.0643
Adenovirus G ANI / AF: 90.3744, 90.8475
```

As expected, they are all pretty similar. Not a tremendous amount of genetic diversity within a given group.

- Compare Adenovirus F vs each other: `./dist_others.sh`. Note, we had to lower `-c` and `-s` quite a bit, much more than the built-in `--small-genomes`.

```
Comparing Adenovirus F to its cousins...
ANI between Adenovirus F and A: 46.2533, 10.14
ANI between Adenovirus F and B: 68.8725, 16.7455
ANI between Adenovirus F and C: 0, 0
ANI between Adenovirus F and D: 76.6281, 19.3789
ANI between Adenovirus F and E: 74.2882, 20.9326
ANI between Adenovirus F and F: 98.3608, 98.6093
ANI between Adenovirus F and G: 76.4716, 24.8242
Comparing Adenovirus F to its cousins...
ANI between Adenovirus F and A: 46.2533, 10.14
ANI between Adenovirus F and B: 68.8725, 16.7455
ANI between Adenovirus F and C: 0, 0
ANI between Adenovirus F and D: 76.6281, 19.3789
ANI between Adenovirus F and E: 74.2882, 20.9326
ANI between Adenovirus F and F: 98.3608, 98.6093
ANI between Adenovirus F and G: 76.4716, 24.8242
```

