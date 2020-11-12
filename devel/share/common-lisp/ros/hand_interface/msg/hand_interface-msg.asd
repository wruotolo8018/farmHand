
(cl:in-package :asdf)

(defsystem "hand_interface-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "flex_sns" :depends-on ("_package_flex_sns"))
    (:file "_package_flex_sns" :depends-on ("_package"))
    (:file "futek_data" :depends-on ("_package_futek_data"))
    (:file "_package_futek_data" :depends-on ("_package"))
  ))