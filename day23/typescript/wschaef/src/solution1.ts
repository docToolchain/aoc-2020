import * as fs from 'fs';

console.info("\n###### Challenge 1 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
const lines = input.split('').map(Number)

class Item{
    public prev?: Item
    public next?: Item
    constructor(
        public value: number,
        public prevValue: number,
        public nextValue: number
        ){}

    setNext(item:Item){
        this.next = item
        this.nextValue = item.value
    }

    setPrev(item:Item){
        this.prev = item
        this.prevValue = item.value
    }
}

class Game{

    public items = new Map<number,Item>()
    private currentItem: Item
    constructor(private input:number[]){
        const length = input.length
        input.forEach((elem,i) => this.items.set(elem,new Item(elem,input[(i-1+length) % length],input[(i+1) % length])))
        input.forEach(value => {
            const item = this.items.get(value) as Item
            item.setPrev(this.items.get(item.prevValue) as Item)
            item.setNext(this.items.get(item.nextValue) as Item)
        })
        this.currentItem = this.items.get(input[0]) as Item
    }

    play(iterations:number):Game{
        for(let i = 0; i < iterations; i++){
            this.move(i)
        }
        return this
    }

    getNextN(n:number): Item{
        let item = this.currentItem
        for(let i=0; i<n; i++){
            item = item.next as Item
        }
        return item
    }

    move(pos: number){
        const pick = [1,2,3].map(n => this.getNextN(n))
        const currentValue = this.currentItem.value

        const destinations = [...this.items.keys()].filter(value => !pick.map(it => it?.value).includes(value))
        let destinationValue = Math.max(...destinations.filter(it => it < currentValue))
        destinationValue = (destinationValue !== -Infinity ? destinationValue : Math.max(...destinations))
        const destination = this.items.get(destinationValue) as Item
        
        pick[0]?.prev?.setNext(pick[2]?.next as Item)
        pick[2]?.next?.setPrev(pick[0]?.prev as Item)
        pick[0].setPrev(destination)
        pick[2].setNext(destination.next as Item)
        destination?.next?.setPrev(pick[2] as Item)
        destination?.setNext(pick[0] as Item)
        this.currentItem = this.currentItem.next as Item
    }
    printString():string{
        const result = []
        let item = this.currentItem
        do{
            result.push(item.value)
            item = item.next as Item
        } while (item.value !== this.currentItem.value) 

        return result.join('')
    }
}
const game = new Game(lines)

const result = game.play(100).printString() 
console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  
 