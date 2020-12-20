import * as fs from 'fs';

console.info("\n###### Challenge 2 #######")
console.time("execution")

const input = fs.readFileSync('input1.txt','utf8');
const lines = input.split('\n')

class Expression{
    public parts = new Array<Expression>()
    public value: number = NaN
    public operator?: string
    constructor(public parent?: Expression|undefined){ 
    }
    public push(token:Expression) {
        this.parts.push(token)
    }
    public evaluate():number{
        if(!isNaN(this.value)){
            return this.value 
        }else{
            const expressionsToDelete:number[] = []
            for(let i=1; i<this.parts.length-1;i+=2){
                if(this.parts[i].operator === '+'){
                    const leftExpr = this.parts[i-1]
                    const rightExpr = this.parts[i+1]
                    const newExpr = new Expression(leftExpr.parent)
                    newExpr.value = leftExpr.evaluate() + rightExpr.evaluate()
                    this.parts[i+1] = newExpr
                    expressionsToDelete.push(i-1)
                    expressionsToDelete.push(i)
                }
            }
            this.parts = this.parts.filter((p,i) => !expressionsToDelete.includes(i))
            for(let i=0; i<this.parts.length;i+=2){
                if(i===0){
                    this.value = this.parts[0].evaluate()
                }else{
                    switch(this.parts[i-1].operator){
                        case '*':
                            this.value = this.value * this.parts[i].evaluate()
                            break;
                    }
                }
            }
        } 
        return this.value
    }
}

function parse(line: string):Expression{
    line = line.split(' ').join('')
    let currentExpr = new Expression()
    for(let i=0; i< line.length; i++){
        const char = line.charAt(i)
        switch (char) {
            case '(':
                const expr = new Expression(currentExpr);
                currentExpr.push(expr)
                currentExpr = expr
                break;
                case ')':
                    currentExpr = currentExpr.parent || currentExpr //should never happen
                break;
            case '*':
                const prodExpr = new Expression(currentExpr);
                prodExpr.operator = char
                currentExpr.push(prodExpr)
                break;
            case '+':
                const plusExpr = new Expression(currentExpr);
                plusExpr.operator = char
                currentExpr.push(plusExpr)
                break;
            default:
                const literalEpr = new Expression(currentExpr);
                literalEpr.value = parseInt(char)
                currentExpr.push(literalEpr)
                break;
        }
    }
    return currentExpr
}

const expressions = lines.map(line => parse(line))
const result = expressions.map(expr => expr.evaluate()).reduce((sum,r)=>sum+r,0)
console.log("RESULT :", result)
console.timeEnd("execution")
console.log("##########################")  
