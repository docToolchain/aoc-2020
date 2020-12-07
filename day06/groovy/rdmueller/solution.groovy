#!/usr/bin/env groovy

//tag::star1[]
result = new File("input.txt").text // read whole file
            .replaceAll("\r","")    // ensure proper line endings
            .split("\n\n").inject(0) { sum, group ->
                def list = [:]
                group.replaceAll("\n","").each { letter ->
                    list[letter]=1
                }
                sum+=list.size()
            }
println result
//end::star1[]

//tag::star2[]
result = new File("input.txt").text // read whole file
            .replaceAll("\r","")    // ensure proper line endings
            .split("\n\n").inject(0) { sum, group ->
                def list = [:]
                group.replaceAll("\n","").each { letter ->
                    list[letter]=list[letter]?list[letter]+1:1
                }
                sum+=list.findAll{it.value==group.split("\n").size()}.size()
            }
println result
//end::star2[]
