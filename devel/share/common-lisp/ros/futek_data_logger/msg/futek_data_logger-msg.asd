
(cl:in-package :asdf)

(defsystem "futek_data_logger-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "futek_data" :depends-on ("_package_futek_data"))
    (:file "_package_futek_data" :depends-on ("_package"))
    (:file "z_pos" :depends-on ("_package_z_pos"))
    (:file "_package_z_pos" :depends-on ("_package"))
  ))