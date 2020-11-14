
(cl:in-package :asdf)

(defsystem "futek_data_logger-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "futek_data" :depends-on ("_package_futek_data"))
    (:file "_package_futek_data" :depends-on ("_package"))
  ))