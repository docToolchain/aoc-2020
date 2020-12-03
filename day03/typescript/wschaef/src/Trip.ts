import {TreeMap} from './TreeMap'

export class Trip{

    private points : string [] = []
    constructor(
        private map: TreeMap,
        private x:number = 0,
        private y:number = 0){
    }
    public move(x:number,y:number){
        this.x = this.x + x
        this.y = this.y + y
        const value = this.map.get(this.x, this.y);
        if ( [".","#"].includes(value)) this.points.push(value)
        return value
    }
    public autoMove(x:number,y:number){
        const value = this.move(x,y)
        if([".","#"].includes(value)){
            this.autoMove(x,y)
        }
        return this.points
    }
}