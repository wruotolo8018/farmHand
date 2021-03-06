// Generated by gencpp from file futek_data_logger/futek_data.msg
// DO NOT EDIT!


#ifndef FUTEK_DATA_LOGGER_MESSAGE_FUTEK_DATA_H
#define FUTEK_DATA_LOGGER_MESSAGE_FUTEK_DATA_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace futek_data_logger
{
template <class ContainerAllocator>
struct futek_data_
{
  typedef futek_data_<ContainerAllocator> Type;

  futek_data_()
    : futek1(0.0)
    , futek2(0.0)  {
    }
  futek_data_(const ContainerAllocator& _alloc)
    : futek1(0.0)
    , futek2(0.0)  {
  (void)_alloc;
    }



   typedef float _futek1_type;
  _futek1_type futek1;

   typedef float _futek2_type;
  _futek2_type futek2;





  typedef boost::shared_ptr< ::futek_data_logger::futek_data_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::futek_data_logger::futek_data_<ContainerAllocator> const> ConstPtr;

}; // struct futek_data_

typedef ::futek_data_logger::futek_data_<std::allocator<void> > futek_data;

typedef boost::shared_ptr< ::futek_data_logger::futek_data > futek_dataPtr;
typedef boost::shared_ptr< ::futek_data_logger::futek_data const> futek_dataConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::futek_data_logger::futek_data_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::futek_data_logger::futek_data_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::futek_data_logger::futek_data_<ContainerAllocator1> & lhs, const ::futek_data_logger::futek_data_<ContainerAllocator2> & rhs)
{
  return lhs.futek1 == rhs.futek1 &&
    lhs.futek2 == rhs.futek2;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::futek_data_logger::futek_data_<ContainerAllocator1> & lhs, const ::futek_data_logger::futek_data_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace futek_data_logger

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::futek_data_logger::futek_data_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::futek_data_logger::futek_data_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::futek_data_logger::futek_data_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::futek_data_logger::futek_data_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::futek_data_logger::futek_data_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::futek_data_logger::futek_data_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::futek_data_logger::futek_data_<ContainerAllocator> >
{
  static const char* value()
  {
    return "0b61dc96ccfbf1e910f406986b9acb9a";
  }

  static const char* value(const ::futek_data_logger::futek_data_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x0b61dc96ccfbf1e9ULL;
  static const uint64_t static_value2 = 0x10f406986b9acb9aULL;
};

template<class ContainerAllocator>
struct DataType< ::futek_data_logger::futek_data_<ContainerAllocator> >
{
  static const char* value()
  {
    return "futek_data_logger/futek_data";
  }

  static const char* value(const ::futek_data_logger::futek_data_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::futek_data_logger::futek_data_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float32 futek1\n"
"float32 futek2\n"
;
  }

  static const char* value(const ::futek_data_logger::futek_data_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::futek_data_logger::futek_data_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.futek1);
      stream.next(m.futek2);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct futek_data_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::futek_data_logger::futek_data_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::futek_data_logger::futek_data_<ContainerAllocator>& v)
  {
    s << indent << "futek1: ";
    Printer<float>::stream(s, indent + "  ", v.futek1);
    s << indent << "futek2: ";
    Printer<float>::stream(s, indent + "  ", v.futek2);
  }
};

} // namespace message_operations
} // namespace ros

#endif // FUTEK_DATA_LOGGER_MESSAGE_FUTEK_DATA_H
