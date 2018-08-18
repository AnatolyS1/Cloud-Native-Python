export default class Tweet extends React.Component {
    render(){
        return(
        <div className="row">
            <form >
                <div className="input-field">
                    <textarea ref="tweetTextArea" className="materializetextarea"/>
                    <label>How you doing?</label>
                    <button className="btn waves-effect waves-lightright">Tweet now 
                    <i className="material-iconsright">send</i></button>
                </div>
            </form>
        </div>
        );
        }
}