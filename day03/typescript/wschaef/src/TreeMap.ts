export class TreeMap {

    private width: number
    private height: number
    constructor(private lines: string[]) { 
        this.width = lines[0]?.length 
        this.height = lines.length
    }

    public get(x:number,y:number){
        if(-1 < y && y > this.height-1) return "x"
        x = x % this.width
        return this.lines[y].charAt(x)
    }
}