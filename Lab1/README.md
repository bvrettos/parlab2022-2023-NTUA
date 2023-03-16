# Lab 1 - Conway's Game of Life

Απλή άσκηση με κύριο σκοπό την εξοικείωσή μας με τα εργαλεία/μηχανήματα του εργαστηρίου. Χρήση του OpenMP για παραλληλοποίηση του αλγορίθμου Game of Life.

O αλγόριθμος δίνεται έτοιμος και εμείς απλά προσθέτουμε το κατάλληλα #pragma directive ώστε να παραλληλοποιηθεί σωστά ο αλγόριθμος χωρίς να έχουμε απώλειες επίδοσης λόγω κακής διαχείρισης shared/copied μεταβλητών.

## Time
<p align="center">
    <img src="plot/time_plots/time_64.png" width="40%" height="40%">
    <img src="plot/time_plots/time_1024.png" width="40%" height="40%">
    <img src="plot/time_plots/time_4096.png" width="40%" height="40%">
</p>


## Speedup
<p align="center">
    <img src="plot/speedup_plots/speedup_64.png" width="40%" height="40%">
    <img src="plot/speedup_plots/speedup_1024.png" width="40%" height="40%">
    <img src="plot/speedup_plots/speedup_4096.png" width="40%" height="40%">
</p>