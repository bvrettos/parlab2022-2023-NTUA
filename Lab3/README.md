# Lab 3 - Mutual Exclusion - Locks

Στο προηγούμενο πρόβλημα που μελετήσαμε, συγκεκριμένα στην υλοποίηση με shared δομή πίνακα, χρησιμοποιούμε το directive **#pragma openmp atomic** για την επίλυση του race-condition. Στην συγκεκριμένη άσκηση, μελετάμε και άλλους τρόπους συγχρονισμού ώστε να υπάρξει mutual exclusion. Μετράμε την επίδοση τους και αποφασίζουμε σε βέλτιστη λύση για το πρόβλημα. Εν τέλει, καταλαβαίνουμε πως να χτίζουμε NUMA-aware, scalable spin-locks και την σημαντικότητα επιλογής σωστού lock για κάθε πρόβλημα.

<p align="center">
    <img src="plots/outFilesAffinityMouliko/plots/kmeans_locks_all.jpg" height="65%" width="65%">
    <img src="plots/outFilesAffinityMouliko/plots/kmeans_locks_all_speedup.jpg" height="65%" width="65%">
</p>

Κυριότερο συμπέρασμα είναι ότι δεν υπάρχει "καλύτερο" lock. Κάθε υλοποίηση έχει λόγο χρήσης, εξαρτάται πάντα από το πρόβλημα που συναντάμε. Μερικές φορές η πιο over-engineered λύση ΔΕΝ είναι και η καλύτερη!