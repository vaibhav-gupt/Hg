(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(inhibit-startup-screen t)
 '(user-full-name "1w6 Team"))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )

(require 'ox-html)
(require 'ox-latex)
;; provide the <k template for a kasten (box)
(add-to-list 'org-structure-template-alist '("k" "#+begin_kasten\n?\n#+end_kasten" "<div class=\"kasten\">?</div>"))
