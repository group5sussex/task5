export class ControlSolutions{
    constructor(nextButton, previousButton, solutionsCount, pyramid, holder){
        this.nextButton = nextButton;
        this.previousButton = previousButton;
        this.solutionsCount = solutionsCount;
        this.pyramid = pyramid;
        this.holder = holder;

        this.solutions = [];
        this.currentSolution = 0;

        this.nextButton.addEventListener("click", this.nextButtonHandler.bind(this));
        this.previousButton.addEventListener("click", this.previousButtonHandler.bind(this));
    }

    addSolution(solution){
        this.solutions.push(solution);
    }

    loadSolution(i){
        if(this.solutions[i]) return;
        this.vBoard = this.solutions[i];
        this.pyramid.loadVirtualBoard(this.vBoard);
    }

    nextButtonHandler(){
        if(this.currentSolution > this.solutions.length - 1) return;
        this.currentSolution++;
        this.updateView();
    }

    previousButtonHandler(){
        if(this.currentSolution < 1) return;
        this.currentSolution--;
        this.updateView()
    }

    updateView(){
        if(!this.solutions) return;
        if(!this.solutions[this.currentSolution]) return;

        this.holder.transform = this.currentSolution===0? "scale(0)": "scaleX(1)";
        this.solutionsCount.innerHTML = this.currentSolution;
        this.loadSolution(this.currentSolution);
        this.previousButton.disabled = this.currentSolution <= 1;
        this.nextButton.disabled = this.currentSolution >= this.solutions.length - 1;
    }

    reset(){
        this.solutions = [];
        this.currentSolution = 0;
        this.updateView();
    }
}