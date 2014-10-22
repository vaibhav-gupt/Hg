#!/usr/bin/env guile-2.0
!#

(define-module (spielfaehig)
  #:export (spielfähig))
(use-modules (srfi srfi-1)) ; for iota with count and start

(define (factorial n)
  (if (zero? n) 1 
      (* n (factorial (1- n)))))

(define (nük n k)
  (if (> k n) 0
      (/ (factorial n) 
         (factorial k) 
         (factorial (- n k)))))

(define (binom p n k)
  (* (nük n k) 
     (expt p k) 
     (expt (- 1 p) (- n k))))

(define (spielfähig p n min_spieler) 
  (apply + 
         (map (lambda (k) (binom p n k)) 
              (iota (1+ (- n min_spieler)) min_spieler))))           


; (format #t "~A\n" (exact->inexact (spielfähig #e.03 4000 70)))
