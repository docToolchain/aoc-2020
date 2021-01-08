import * as fs from 'fs';

console.info("\n###### Challenge 2 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
const lines = input.split('').map(Number)

class Item{
    public next?: Item
    constructor(
        public value: number,
        public nextValue: number
        ){}

    setNext(item:Item){
        this.next = item
        this.nextValue = item.value
    }

}

class Game{

    public items = new Map<number,Item>()
    private currentItem: Item
    constructor(private input:number[]){
        const length = input.length
        input.forEach((elem,i) => this.items.set(elem,new Item(elem,input[(i+1) % length])))
        input.forEach(value => {
            const item = this.items.get(value) as Item
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
        const pickValues = pick.map(item => item.value)
        const currentValue = this.currentItem.value

        const minPick = Math.min(...pickValues)
        const minValue = minPick > 1 ? 1 : pickValues.includes(2) ? pickValues.includes(3) ? 4 : 3 : 2

        let destinationValue = currentValue - 1

        while (destinationValue > minValue && pickValues.includes(destinationValue)){
            destinationValue--
        }
        if (destinationValue < minValue){
            const maxPickValue = Math.max(...pickValues)
            const itemsSize = this.items.size
            destinationValue = maxPickValue < itemsSize ? itemsSize : pickValues.includes(itemsSize - 1) ? pickValues.includes(itemsSize - 2) ? itemsSize - 3 : itemsSize - 2 : itemsSize - 1 
        }

        const destination = this.items.get(destinationValue) as Item
        
        this.currentItem.setNext(pick[2].next as Item)
        this.currentItem = pick[2].next as Item
        pick[2].setNext(destination.next as Item)
        destination?.setNext(pick[0] as Item)
    }
}

const inputList = Array.from(Array(1000000).keys()).map(it => it < 9 ? lines[it]:it+1)
const game = new Game(inputList)
game.play(10000000)

const result = [(game.items.get(1)?.nextValue as number),(game.items.get(1)?.next?.nextValue as number)]
console.log("RESULT :", result, result[0] * result[1])
console.timeEnd("execution")
console.log("##########################")  
 