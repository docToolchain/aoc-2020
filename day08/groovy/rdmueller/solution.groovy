#!/usr/bin/env groovy
import cpu.*

//tag::star1[]
Parser.parse(new File("input.txt").text)
try {
    Vm.run()
} catch (Exception e) {
    println e.message
}
//end::star1[]

//tag::star2[]
def line = 0
while (1==1) {
    Parser.parse(new File("input.txt").text)
    if (Vm.program[line].op!='acc') {
        if (Vm.program[line].op=='jmp') {
            Vm.program[line].op='nop'
        } else {
            Vm.program[line].op='jmp'
        }
        try {
            Vm.run()
        } catch (Exception e) {
            if (e.message.startsWith("terminated")) {
                println e.message
                throw new Exception("finished")
            }
        }
    } 
    line++
    
}
//end::star2[]
