import './SinglePageReviewStyles.css'
import { FaStar } from "react-icons/fa";

const SinglePageReviewSection: React.FC = () => {
    return (
      <div className='review-main-sec' >
        <p className='reviews-title'>Reviews</p>
        <div className="rating-sec">
            <div className="rating-sec-inner">
                <h2>4.47</h2>
                <p className="gray-p">/5</p>
            </div>
            <p className="gray-p">3 Verified review</p>
        </div>
        <p className='reviews-title'>Comments</p>
        <div className="review-comments-sec">
            <div className="review">
                <p className="review-username">username</p>
                <p className="review-date gray-p">February 8, 2023</p>
                <div>
                    <FaStar color="yellow"/>
                    <FaStar color="yellow"/>
                    <FaStar color="yellow"/>
                    <FaStar color="yellow"/>
                </div>
                <p className="comment">We always stay at here when in town. The location is great, staff is wonderful and we love the overall feel. Beautiful view from the here.</p>
            </div>
            <hr />
            <div className="review">
                <p className="review-username">username</p>
                <p className="review-date gray-p">February 8, 2023</p>
                <div>
                    <FaStar color="yellow"/>
                    <FaStar color="yellow"/>
                    <FaStar color="yellow"/>
                </div>
                <p className="comment">We always stay at here when in town. The location is great, staff is wonderful and we love the overall feel. Beautiful view from the here.</p>
            </div>
            <hr />
            <div className="review">
                <p className="review-username">username</p>
                <p className="review-date gray-p">February 8, 2023</p>
                <div>
                    <FaStar color="yellow"/>
                    <FaStar color="yellow"/>
                    <FaStar color="yellow"/>
                    <FaStar color="yellow"/>
                </div>
                <p className="comment">We always stay at here when in town. The location is great, staff is wonderful and we love the overall feel. Beautiful view from the here.</p>
            </div>
        </div>
      </div>
    );
  }
  
  export default SinglePageReviewSection;