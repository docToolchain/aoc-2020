import * as fs from 'fs';

console.info("\n###### Challenge 2 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8'); 
const blocksStr = input.split('mask = ').filter(it=>it).map(b => b.split('\n')).filter(it => it)

class Block{

    private mask: string
    private commands: number[][]

    constructor(private block: string[]){
        block = block.filter(it=>it)
        this.mask = block[0]
        this.commands = block.slice(1)
                .map(it => /mem\[(\d+)\] = ([^ ]*)/.exec(it))
                .map(regex => [regex?.[1],regex?.[2]])
                .map(([mem,value]) => [parseInt(mem || '-1'),parseInt(value ||'-1')]) 
    }

    private executeInstr(command: number[],memory:Memory){
        const [mem,value] = command
        const memAddrBits = Memory.toBin(mem,36).split('')
        const newMask = this.mask.split('').map((bit,i) => bit === '0'?memAddrBits[i]:bit).join('')
        let addresses = new Array<Array<string>>()
        addresses.push(new Array<string>())
        newMask.split('').forEach(bit => {
            if(bit !== 'X'){
                addresses.forEach(it => it.push(bit))
            }else{
                const addressesCopy = addresses.map(it => [...it])
                addresses.forEach(it => it.push('0'))
                addressesCopy.forEach(it => it.push('1'))
                addresses = addresses.concat(addressesCopy)
            }
        })
        const newAddresses = addresses.map(a => Memory.fromBin(a.join('')))
        newAddresses.forEach(address => memory.update(address,Memory.toBin(value,36)))
    }

    public execute(memory: Memory){
        this.commands.forEach(cmd => this.executeInstr(cmd,memory))
    }
}
class MemoryEntry{
    constructor(public address:number, public value:string){}
}
class Memory{

    private entries = new Array<MemoryEntry>()
    
    public update(address:number,value:string){
        let entry = this.entries.find(it=>it.address === address)
        if(!entry){
            this.entries.push(new MemoryEntry(address,value))
        }else{
            entry.value = value
        } 
    }

    public static toBin(n:number,length:number):string{
        return n.toString(2).padStart(length,'0')
    }
    public static fromBin(n:string):number{
        return parseInt(n,2)
    }

    public getSum(){
        return this.entries.reduce((sum,it)=>Memory.fromBin(it.value)+sum,0)
    }
}
class Programm{

    private memory = new Memory()    

    constructor(private blocks: Block[]){}

    public executeBlock(block:Block){
        block.execute(this.memory)
        return this.memory
    }

    public execute():Memory{
        this.blocks.map(b => this.executeBlock(b))
        return this.memory
    }
}

const programm = new Programm(blocksStr.map(it => new Block(it)))
const memory = programm.execute()

const result = memory.getSum()
console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  
