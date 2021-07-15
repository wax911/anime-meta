## :penguin: :snake: anime-meta :penguin: :snake:

A personal project for generating an anime database using MongoDB, this project solely exists as a learning experience
for applying OOP principles like DI, Abstraction, Inheritance and Polymorphism in python with an emphasis on type hints.

### Architecture

This project adopts techniques typically found in [clean architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html), thus all
network models used to fetch data from the sample api are only used internally in the **data** layer, while application specific models (aka entities) can 
be found in the **domain** layer.

### Dependencies
- pymongo
- uplink
- dacite
- mongo-thingy
- requests_oauthlib
- dependency_injector
- PyYAML
- asyncio
- marshmallow

### License
```
Copyright 2019 wax911

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
