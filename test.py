import time
import progressbar

widgets = [
    ' [', progressbar.DataSize(), '] ',
    progressbar.Bar(),
    ' (', progressbar.ETA(), ') ',
]

bar = progressbar.ProgressBar(max_value=100, redirect_stdout=True, widgets=widgets)
for i in range(100):
    print('Some text', i)
    time.sleep(0.1)
    bar.update(i)
