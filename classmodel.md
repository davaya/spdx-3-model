# The Class Model
This document describes the Class method of defining logical data models in a manner that facilitates
representing logical values as serialized physical data. The first obstacle to describing the
method is terminology; several terms used are heavily overloaded and subject to differing
opinions as to meaning. Within this document they mean:

## Terminology

* **Class** - the name of a set of features used to distinguish some instances from others.
* **Classifier** - a classification of instances according to their features --- [UML](#uml) Section 9.  
* **Instance** - a logical or physical data item identified by a classifier as being a member of a class.
* **Type** - an exact synonym for class; type and class are used interchangeably here.
* **Logical Value** - instances with meaning defined by the model
* **Physical Value** - a sequence of bytes that represents a logical value using a specific data format

In object-oriented programming a class can have public variables, private variables, and methods.
A class model MAY be implemented using OOP classes where logical values are the public variables of a class,
but this document does not constrain or assume that implementations of the class model are OOP-based.

## Principles
1. Every class is based on one of a set of pre-defined root ("base") classes.
2. There are two kinds of [base class](https://www.w3.org/TR/xmlschema11-1/#Type_Definition_Summary)
(XSD): simple ("primitive") and complex ("compound"). Simple class instances are atomic values that
cannot be decomposed, complex class instances are containers with container type and content.
3. There are two kinds of complex class: datatype and classtype.
    * [Datatype](#uml) (UML Section 10.2) instances are distinguished only by their value.
    * Classtype* instances are distinguished by a subset of their value, called a key or id.

Simple classes are by definition datatypes because there is no subset of a simple instance's
value.  So each class is one of: simple datatype, complex datatype, or complex classtype.

 *\* Classtype is used in this document as the name for "every class that is not a datatype".*

## Simple Classes

## Complex Classes

All complex classes have four [multiplicity attributes](#uml) (UML Section 7.5):
* minCount
* maxCount
* isUnique
* isOrdered

|  Container | isUnique | isOrdered |
|-----------:|:--------:|:---------:|
|        Set |   true   |   false   |
| OrderedSet |   true   |   true    |
|   Sequence |  false   |   true    |
|        Bag |  false   |   false   |

Complex classes that enumerate fields by identifier and class/type are always unique (Set or OrderedSet) -
there must not be duplicate field identifiers within a class. There can be duplicate member instances,
for example a class with "start" and "end" fields, each with the same value class/type.)

In complex classes with no field identifiers, all members have the same value class/type and the container
may be any of the four container types.


## References
###### [UML]

*Unified Modeling Language*, Object Management Group, Version 2.5.1, December 2017,
https://www.omg.org/spec/UML/2.5.1/PDF

###### [XSD]

*W3C XML Schema Definition Language*, 1.1 Part 1, W3C Recommendation 5 April 2012,
https://www.w3.org/TR/xmlschema11-1/